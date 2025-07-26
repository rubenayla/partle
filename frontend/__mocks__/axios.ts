import { vi } from 'vitest';

const axios = vi.fn(() => Promise.resolve({ data: {} }));
axios.create = vi.fn(() => axios);
axios.get = vi.fn(() => Promise.resolve({ data: {} }));
axios.post = vi.fn(() => Promise.resolve({ data: {} }));
axios.put = vi.fn(() => Promise.resolve({ data: {} }));
axios.delete = vi.fn(() => Promise.resolve({ data: {} }));

axios.interceptors = {
  request: {
    use: vi.fn(),
    eject: vi.fn(),
  },
  response: {
    use: vi.fn(),
    eject: vi.fn(),
  },
};

export default axios;