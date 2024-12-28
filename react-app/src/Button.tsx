import { useState } from "react";

interface Props {
  children: string[];
  color?: "primary" | "secondary" | "danger";
  onClick: () => void;
}

// ALWAYS use PascalCasing
function Button({ children, color = "primary", onClick }: Props) {
  return (
    <button type="button" className={"btn btn-" + color} onClick={onClick}>
      {children}
    </button>
  );
}

export default Button;
