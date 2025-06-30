import { ReactNode, useState } from 'react';

interface Props {
  children: ReactNode;
  text: string;
}

export default function Tooltip({ children, text }: Props) {
  const [visible, setVisible] = useState(false);

  return (
    <div
      className="tooltip-container"
      onMouseEnter={() => setVisible(true)}
      onMouseLeave={() => setVisible(false)}
    >
      {children}
      {visible && <div className="tooltip">{text}</div>}
    </div>
  );
}