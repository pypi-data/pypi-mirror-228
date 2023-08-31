import os
import tarfile

from tqdm import tqdm


class TarFile(tarfile.TarFile):
    def __init__(self, name=None, mode="r", fileobj=None, format=None, tarinfo=None, dereference=None,
                 ignore_zeros=None, encoding=None, errors="surrogateescape", pax_headers=None, debug=None,
                 errorlevel=None, copybufsize=None):
        self._progress_callback = None
        super(TarFile, self).__init__(name=name, mode=mode, fileobj=fileobj, format=format, tarinfo=tarinfo,
                                      dereference=dereference, ignore_zeros=ignore_zeros, encoding=encoding,
                                      errors=errors, pax_headers=pax_headers, debug=debug, errorlevel=errorlevel,
                                      copybufsize=copybufsize)

    def get_progress(self, size, desc='') -> tqdm:
        desc = os.path.basename(desc)
        if self._progress_callback is not None:
            self._progress_callback.total += size
            return self._progress_callback

        res = tqdm(total=size, unit='B', desc=desc, ascii=True, unit_scale=True)
        self._progress_callback = res
        return res

    def addfile(self, tarinfo, fileobj=None):
        if fileobj is not None:
            fileobj = FileWrapper(fileobj, self.get_progress(tarinfo.size, desc=tarinfo.name))
        result = super(TarFile, self).addfile(tarinfo, fileobj)
        self.close_progress()
        return result

    def close_progress(self):
        if self._progress_callback is not None:
            self._progress_callback.close()

    def extractall(self, path=".", members=None, **kwargs):
        result = super(TarFile, self).extractall(path, members, **kwargs)
        self.close_progress()
        return result

    def extract(self, member, path="", **kwargs):
        return super(TarFile, self).extract(member=member, path=path, **kwargs)

    def extractfile(self, member):
        return super(TarFile, self).extractfile(member)


class FileWrapper(object):
    def __init__(self, fileobj, progress: tqdm):
        self._fileobj = fileobj
        self._progress = progress

    def _update(self, length):
        if self._progress is not None:
            if self._progress.n + length > self._progress.total:
                self._progress.total = self._progress.n + length

            self._progress.update(length)
            self._progress.refresh()

    def read(self, size=-1):
        data = self._fileobj.read(size)
        self._update(len(data))
        return data

    def readline(self, size=-1):
        data = self._fileobj.readline(size)
        self._update(len(data))
        return data

    def __getattr__(self, name):
        return getattr(self._fileobj, name)

    def __del__(self):
        self._update(0)


open = TarFile.open
