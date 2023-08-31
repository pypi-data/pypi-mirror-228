import mock
from ixtest.mock import Mut, create_mock

from ixoncdkingress import utils as sut

def test_handle_reload_exception(monkeypatch):
    mut = Mut(sut.handle_exception)

    mut.exception = create_mock(name='exception')
    mut.exception.__traceback__ = 'my tracback'

    mut.create_test_suite(monkeypatch)

    mut()

    assert [
        mock.call(None, mut.exception, mut.exception.__traceback__)
    ] == sut.traceback.print_exception.call_args_list
    assert sut.ResponseCode.INTERNAL_ERROR == mut.response.status_code
