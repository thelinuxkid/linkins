import mock
import subprocess

from linkins import script
from linkins.test import util

@mock.patch('linkins.script.log')
@mock.patch('subprocess.Popen')
def test_runscript_simple(fakepopen, fakelog):
    proc = fakepopen.return_value
    err_manager = proc.stderr.__enter__.return_value
    err_manager.__iter__.return_value = ['foo stderr']
    out_manager = proc.stdout.__enter__.return_value
    out_manager.__iter__.return_value = ['foo stdout']
    script.runscript('/foo/bar')

    popen = util.mock_call_with_name(
        '',
        ['/foo/bar'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )
    err_enter = util.mock_call_with_name(
        '().stderr.__enter__',
        )
    err_iter_ = util.mock_call_with_name(
        '().stderr.__enter__().__iter__',
    )
    err_exit = util.mock_call_with_name(
        '().stderr.__exit__',
        None,
        None,
        None,
    )
    out_enter = util.mock_call_with_name(
        '().stdout.__enter__',
        )
    out_iter_ = util.mock_call_with_name(
        '().stdout.__enter__().__iter__',
    )
    out_exit = util.mock_call_with_name(
        '().stdout.__exit__',
        None,
        None,
        None,
    )
    err_log = util.mock_call_with_name(
        'info',
        'foo stderr',
        extra={'stream': 'STDERR', 'script': 'bar'},
        )
    out_log = util.mock_call_with_name(
        'info',
        'foo stdout',
        extra={'stream': 'STDOUT', 'script': 'bar'},
        )
    popen_calls = [
        popen,
        err_enter,
        err_iter_,
        err_exit,
        out_enter,
        out_iter_,
        out_exit,
    ]
    log_calls = [
        err_log,
        out_log,
        ]
    assert fakepopen.mock_calls == popen_calls
    assert fakelog.mock_calls == log_calls

@mock.patch('linkins.script.log')
@mock.patch('subprocess.Popen')
def test_runscript_args(fakepopen, fakelog):
    script.runscript('/foo/bar', 'fee', 'fi', 'fo')
    popen = util.mock_call_with_name(
        '',
        ['/foo/bar', 'fee', 'fi', 'fo'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        )
    err_enter = util.mock_call_with_name(
        '().stderr.__enter__',
        )
    err_iter_ = util.mock_call_with_name(
        '().stderr.__enter__().__iter__',
    )
    err_exit = util.mock_call_with_name(
        '().stderr.__exit__',
        None,
        None,
        None,
    )
    out_enter = util.mock_call_with_name(
        '().stdout.__enter__',
        )
    out_iter_ = util.mock_call_with_name(
        '().stdout.__enter__().__iter__',
    )
    out_exit = util.mock_call_with_name(
        '().stdout.__exit__',
        None,
        None,
        None,
    )
    popen_calls = [
        popen,
        err_enter,
        err_iter_,
        err_exit,
        out_enter,
        out_iter_,
        out_exit,
    ]
    assert fakepopen.mock_calls == popen_calls
    assert fakelog.mock_calls == []
