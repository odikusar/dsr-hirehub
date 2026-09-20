import { useState } from "react";
import { Test2Component } from "./test2Component";

export function TestComponent() {

  const [counter, setCounter] = useState(100);
  const fn = function () {
    alert("Hello");
    setCounter(counter + 1);
  }

  return (
    <div className="hello">
      <button onClick={() => fn()}>
        Click me
      </button>
      {counter}<br />
      <Test2Component counter={counter}></Test2Component>
    </div>
  );
}
