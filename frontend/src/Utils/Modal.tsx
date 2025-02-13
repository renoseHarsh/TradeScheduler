interface ModalProps {
  onClose: () => void;
  children?: React.ReactNode;
}

export default function Modal({ onClose, children }: ModalProps) {
  return (
    <div
      onClick={onClose}
      className="z-50 visible fixed inset-0 flex items-center justify-center bg-black/20 transition-colors"
    >
      <div onClick={(e) => e.stopPropagation()}>{children}</div>
    </div>
  );
}
