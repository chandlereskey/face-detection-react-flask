import { ReactNode } from "react";

interface Props {
  children: ReactNode;
  onClose: () => void;
}

export default function Alert({ children, onClose }: Props) {
  return (
    <>
      <div className="alert alert-primary alert-dismissable">{children}</div>
      <button
        type="button"
        className="btn-close"
        data-bs-dismiss="alert"
        onClick={() => onClose()}
      />
    </>
  );
}
