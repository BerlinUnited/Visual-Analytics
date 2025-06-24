import { Store } from '@tanstack/react-store';

// Initial state
const initialState = {
  counter: 0,
  user: null,
  // add other state properties as needed
};

// Create the store
export const store = new Store(initialState);