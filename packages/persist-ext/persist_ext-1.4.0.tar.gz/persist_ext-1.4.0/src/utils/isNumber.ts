export function isNumber(obj: unknown): obj is number {
  return typeof obj === 'number' && isFinite(obj);
}
