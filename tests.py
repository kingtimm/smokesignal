""" Unit tests """
from unittest import TestCase

from mock import Mock

import smokesignal


class SmokesignalTestCase(TestCase):

    def setUp(self):
        self.callback = lambda x: x
        self.mock_callback = Mock()

    def tearDown(self):
        smokesignal.clear_all()

    def test_clear(self):
        smokesignal.on('foo', self.callback)
        assert len(smokesignal.receivers['foo']) == 1

        smokesignal.clear('foo')
        assert len(smokesignal.receivers['foo']) == 0

    def test_clear_all(self):
        smokesignal.on('foo', self.callback)
        smokesignal.on('bar', self.callback)
        assert len(smokesignal.receivers['foo']) == 1
        assert len(smokesignal.receivers['bar']) == 1

        smokesignal.clear_all()
        assert len(smokesignal.receivers['foo']) == 0
        assert len(smokesignal.receivers['bar']) == 0

    def test_emit_with_no_callbacks(self):
        smokesignal.emit('foo')

    def test_emit_with_callbacks(self):
        # Register first
        smokesignal.on('foo', self.mock_callback)
        assert self.mock_callback in smokesignal.receivers['foo']

        smokesignal.emit('foo')
        assert self.mock_callback.called

    def test_emit_with_callback_args(self):
        # Register first
        smokesignal.on('foo', self.mock_callback)
        assert self.mock_callback in smokesignal.receivers['foo']

        smokesignal.emit('foo', 1, 2, 3, foo='bar')
        assert self.mock_callback.called_with(1, 2, 3, foo='bar')

    def test_on_raises(self):
        self.assertRaises(AssertionError, smokesignal.on, 'foo', None)

    def test_on_registers(self):
        smokesignal.on('foo', self.callback)
        assert self.callback in smokesignal.receivers['foo']

    def test_disconnect(self):
        # Register first
        smokesignal.on('foo', self.callback)
        assert self.callback in smokesignal.receivers['foo']

        # Remove it
        smokesignal.disconnect('foo', self.callback)
        assert self.callback not in smokesignal.receivers['foo']

    def test_once_raises(self):
        self.assertRaises(AssertionError, smokesignal.once, 'foo', None)

    def test_once(self):
        # Make a method that has a call count
        def cb():
            cb.call_count += 1
        cb.call_count = 0

        # Register first
        smokesignal.once('foo', cb)
        assert len(smokesignal.receivers['foo']) == 1

        # Call twice
        smokesignal.emit('foo')
        smokesignal.emit('foo')

        assert cb.call_count == 1
