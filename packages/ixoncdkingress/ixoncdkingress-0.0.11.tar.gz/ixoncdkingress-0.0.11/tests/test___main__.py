import mock, pytest

from ixtest.mock import Mut

from ixoncdkingress import __main__ as sut

def test_main_ok(monkeypatch):
    mut = Mut(sut.main)

    mut.create_test_suite(monkeypatch)

    out_put = mut()

    config = sut.Config.from_environ.return_value
    servlet = sut.Servlet.return_value

    assert 0 == out_put

    assert [
        mock.call(sut.os.environ)
    ] == sut.Config.from_environ.call_args_list

    assert [
        mock.call(sut.Config.from_environ.return_value)
    ] == sut.Servlet.call_args_list

    assert [
        mock.call(config, servlet)
    ] == sut.wsgi.run_server.call_args_list

def test_main_ki(monkeypatch):
    mut = Mut(sut.main)

    mut.create_test_suite(monkeypatch)

    sut.wsgi.run_server.side_effect = KeyboardInterrupt

    out_put = mut()

    assert 0 == out_put

def test_main_ie(monkeypatch):
    mut = Mut(sut.main)

    mut.create_test_suite(monkeypatch)

    sut.wsgi.run_server.side_effect = IndexError

    with pytest.raises(IndexError):
        out_put = mut()

        assert 0 == out_put
