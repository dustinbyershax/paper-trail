/**
 * Debounce utility for delaying function execution.
 * Useful for search inputs to avoid excessive URL updates.
 */

/**
 * Creates a debounced function that delays execution until after the wait period.
 * Subsequent calls reset the timer.
 *
 * @param func - Function to debounce
 * @param wait - Delay in milliseconds
 * @returns Debounced function
 */
export function debounce<T extends (...args: any[]) => any>(
  func: T,
  wait: number
): (...args: Parameters<T>) => void {
  let timeout: ReturnType<typeof setTimeout> | null = null;

  return function (this: any, ...args: Parameters<T>) {
    if (timeout) clearTimeout(timeout);
    timeout = setTimeout(() => func.apply(this, args), wait);
  };
}
