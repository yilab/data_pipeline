import datetime
import errno
import fileinput
import gzip
import json
import os


class CompressedStreamRotator(object):

    def __init__(self):
        self.file_start_time = None
        self.output_file = None

    def run(self):
        try:
            self._compress_streaming_json()
        except IOError as e:
            if e.errno == errno.EPIPE:
                # just stop if the pipe breaks
                pass
        finally:
            self._close_file()

    def _compress_streaming_json(self):
        for line in fileinput.input():
            line = line.strip()
            self._process_line(line)

    def _process_line(self, line):
        self._update_output_file_for_timestamp(json.loads(line)['timestamp'])
        self.output_file.write(line)
        self.output_file.write("\n")

    def _update_output_file_for_timestamp(self, timestamp):
        current_time = datetime.datetime.fromtimestamp(timestamp)
        if not self._belongs_in_current_file(current_time):
            print current_time, self.file_start_time
            self._close_file()
            self._create_complete_file_if_needed(current_time)
            self._open_file(current_time)

    def _belongs_in_current_file(self, current_time):
        return (
            self.file_start_time is not None and
            current_time < self._get_file_end_time() and
            self._file_date_matches_current_time(current_time)
        )

    def _file_date_matches_current_time(self, current_time):
        return self.file_start_time is not None and self.file_start_time.date() >= current_time.date()

    def _create_complete_file_if_needed(self, current_time):
        if self.file_start_time is not None and not self._file_date_matches_current_time(current_time):
            with open(os.path.join(self._get_current_file_path(), 'COMPLETE'), 'w'):
                # Just create the file
                pass

    def _get_current_file_path(self):
        return os.path.abspath(self.file_start_time.date().strftime("%Y/%m/%d"))

    def _get_file_end_time(self):
        return self.file_start_time + datetime.timedelta(minutes=15)

    def _ensure_current_path_exists(self):
        if not os.path.exists(self._get_current_file_path()):
            os.makedirs(self._get_current_file_path())

    def _open_file(self, start_time):
        self.file_start_time = start_time
        self._ensure_current_path_exists()

        file_name = "%s.json.gz" % start_time.isoformat()
        file_path = os.path.join(self._get_current_file_path(), file_name)
        self.output_file = gzip.open(file_path, 'wb', 3)

    def _close_file(self):
        if self.output_file is not None:
            self.output_file.close()
        self.output_file = None


if __name__ == "__main__":
    CompressedStreamRotator().run()
