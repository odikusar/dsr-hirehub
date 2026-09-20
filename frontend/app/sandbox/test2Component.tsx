import { useEffect, useRef } from "react";


export function Test2Component({ counter }: { counter: number }) {


  const isFirst = useRef(true);

  useEffect(() => {
    if (isFirst.current) { isFirst.current = false; return; }
    // alert("EFFECT !!!");
  }, [counter]);

  return (
    <div className="hello">
        {counter}
    </div>
  );
}
