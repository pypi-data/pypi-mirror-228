import mock
from ixtest.mock import Mut, create_mock

from ixoncdkingress import types as sut

def test_response_code_status_line(monkeypatch):
    mut = Mut(sut.ResponseCode.status_line)
    mut.self = create_mock(name='self')

    mut.create_test_suite(monkeypatch)

    out_put = mut()

    assert f"{mut.self.value} {mut.self.name.replace.return_value}" == out_put

    assert [
        mock.call('_', ' ')
    ] == mut.self.name.replace.call_args_list
