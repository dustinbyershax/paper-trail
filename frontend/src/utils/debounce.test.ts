import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { debounce } from './debounce';

describe('debounce', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('delays function execution', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 500);

    debounced('test');
    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(499);
    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1);
    expect(fn).toHaveBeenCalledTimes(1);
    expect(fn).toHaveBeenCalledWith('test');
  });

  it('cancels previous timeout when called again', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 500);

    debounced('first');
    vi.advanceTimersByTime(300);
    debounced('second');
    vi.advanceTimersByTime(300);
    expect(fn).not.toHaveBeenCalled();

    vi.advanceTimersByTime(200);
    expect(fn).toHaveBeenCalledTimes(1);
    expect(fn).toHaveBeenCalledWith('second');
  });

  it('handles multiple arguments', () => {
    const fn = vi.fn();
    const debounced = debounce(fn, 500);

    debounced('arg1', 'arg2', 123);
    vi.advanceTimersByTime(500);

    expect(fn).toHaveBeenCalledWith('arg1', 'arg2', 123);
  });

  it('preserves function context', () => {
    const obj = {
      value: 42,
      method: vi.fn(function (this: { value: number }) {
        return this.value;
      }),
    };

    const debounced = debounce(obj.method, 500);
    debounced.call(obj);
    vi.advanceTimersByTime(500);

    expect(obj.method).toHaveBeenCalled();
  });

  it('allows multiple debounced instances', () => {
    const fn1 = vi.fn();
    const fn2 = vi.fn();
    const debounced1 = debounce(fn1, 300);
    const debounced2 = debounce(fn2, 500);

    debounced1('first');
    debounced2('second');

    vi.advanceTimersByTime(300);
    expect(fn1).toHaveBeenCalledWith('first');
    expect(fn2).not.toHaveBeenCalled();

    vi.advanceTimersByTime(200);
    expect(fn2).toHaveBeenCalledWith('second');
  });
});
