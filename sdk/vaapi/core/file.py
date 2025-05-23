import typing

# File typing inspired by the flexibility of types within the httpx library
# https://github.com/encode/httpx/blob/master/httpx/_types.py
FileContent = typing.Union[typing.IO[bytes], bytes, str]
File = typing.Union[
    # file (or bytes)
    FileContent,
    # (filename, file (or bytes))
    typing.Tuple[typing.Optional[str], FileContent],
    # (filename, file (or bytes), content_type)
    typing.Tuple[typing.Optional[str], FileContent, typing.Optional[str]],
    # (filename, file (or bytes), content_type, headers)
    typing.Tuple[
        typing.Optional[str],
        FileContent,
        typing.Optional[str],
        typing.Mapping[str, str],
    ],
]


def convert_file_dict_to_httpx_tuples(
    d: typing.Dict[str, typing.Union[File, typing.List[File]]],
) -> typing.List[typing.Tuple[str, File]]:
    """
    The format we use is a list of tuples, where the first element is the
    name of the file and the second is the file object. Typically HTTPX wants
    a dict, but to be able to send lists of files, you have to use the list
    approach (which also works for non-lists)
    https://github.com/encode/httpx/pull/1032
    """

    httpx_tuples = []
    for key, file_like in d.items():
        if isinstance(file_like, list):
            for file_like_item in file_like:
                httpx_tuples.append((key, file_like_item))
        else:
            httpx_tuples.append((key, file_like))
    return httpx_tuples
