// Test hook to debug React context issue
import { useState } from 'react';

export function useTest() {
  console.log('useTest: Attempting useState call');
  const [test, setTest] = useState('test');
  console.log('useTest: useState succeeded');
  return [test, setTest];
}