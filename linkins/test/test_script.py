import mock
import subprocess

from linkins import script
from linkins.test import util

@mock.patch('multiprocessing.Process')
@mock.patch('linkins.script.log')
@mock.patch('subprocess.Popen')
def test_runscript_simple(fakepopen, fakelog, fakeprocess):
    proc = fakepopen.return_value
    poll = proc.poll
    poll.return_value = 0
    read = proc.stdout.read
    read.side_effect = iter('foo\n')
    script.runscript('/foo/bar')

    popen = util.mock_call_with_name(
        '',
        ['/foo/bar'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        )
    read = mock.call().stdout.read(1)
    reads = [read]*5
    close = mock.call().stdout.close()
    out_log = util.mock_call_with_name(
        'info',
        'foo',
        extra={'source': 'SCRIPT', 'script': 'bar'},
        )
    popen_calls = [
        popen,
    ]
    popen_calls += reads
    popen_calls.append(close)
    log_calls = [
        out_log,
        ]
    assert fakepopen.mock_calls == popen_calls
    assert fakelog.mock_calls == log_calls
    assert fakeprocess.mock_calls == []

@mock.patch('multiprocessing.Process')
@mock.patch('linkins.script.log')
@mock.patch('subprocess.Popen')
def test_runscript_args(fakepopen, fakelog, fakeprocess):
    proc = fakepopen.return_value
    poll = proc.poll
    poll.return_value = 0
    read = proc.stdout.read
    read.side_effect = iter('')
    script.runscript('/foo/bar', 'fee', 'fi', 'fo')

    popen = util.mock_call_with_name(
        '',
        ['/foo/bar', 'fee', 'fi', 'fo'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        )
    read = mock.call().stdout.read(1)
    close = mock.call().stdout.close()
    popen_calls = [
        popen,
        read,
        close,
    ]
    assert fakepopen.mock_calls == popen_calls
    assert fakelog.mock_calls == []
    assert fakeprocess.mock_calls == []

@mock.patch('multiprocessing.Process')
@mock.patch('linkins.script.log')
@mock.patch('subprocess.Popen')
def test_runscript_name(fakepopen, fakelog, fakeprocess):
    proc = fakepopen.return_value
    poll = proc.poll
    poll.return_value = 0
    read = proc.stdout.read
    read.side_effect = iter('foo\n')
    script.runscript('/foo/bar', name='foo-name')

    popen = util.mock_call_with_name(
        '',
        ['/foo/bar'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True,
        )
    read = mock.call().stdout.read(1)
    reads = [read]*5
    close = mock.call().stdout.close()
    out_log = util.mock_call_with_name(
        'info',
        'foo',
        extra={'source': 'SCRIPT', 'script': 'foo-name'},
        )
    popen_calls = [
        popen,
    ]
    popen_calls += reads
    popen_calls.append(close)
    log_calls = [
        out_log,
        ]
    assert fakepopen.mock_calls == popen_calls
    assert fakelog.mock_calls == log_calls
    assert fakeprocess.mock_calls == []

@mock.patch('multiprocessing.Process')
@mock.patch('linkins.script.log')
@mock.patch('subprocess.Popen')
def test_runscript_multiprocess(fakepopen, fakelog, fakeprocess):
    script.runscript('/foo/bar', multiprocess=True)
    assert fakepopen.mock_calls == []
    assert fakelog.mock_calls == []
    process = mock.call(
        target=script._run,
        args=(['/foo/bar'], 'bar'),
        )
    start = mock.call().start()
    calls = [
        process,
        start,
        ]
    assert fakeprocess.mock_calls == calls
