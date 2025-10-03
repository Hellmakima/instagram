"use client";
import { useDispatch, useSelector } from "react-redux";
import { decrement, increment } from "@/lib/store/slice";
import { AppDispatch, RootState } from "@/lib/store/store";

export default function TryRedux() {
  const count = useSelector((state: RootState) => state.counter.value);
  const dispatch = useDispatch<AppDispatch>();
  return (
    <div>
      <div>
        <button
          aria-label="Increment value"
          onClick={() => dispatch(increment())}
        >
          Increment
        </button>
        <span>{count}</span>
        <button
          aria-label="Decrement value"
          onClick={() => dispatch(decrement())}
        >
          Decrement
        </button>
      </div>
    </div>
  );
}
