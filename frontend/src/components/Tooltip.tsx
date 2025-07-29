
import * as TooltipPrimitive from '@radix-ui/react-tooltip';
import { ReactNode } from 'react';

interface Props {
  children: ReactNode;
  text: string;
}

export default function Tooltip({ children, text }: Props) {
  return (
    <TooltipPrimitive.Provider>
      <TooltipPrimitive.Root>
        <TooltipPrimitive.Trigger asChild>{children}</TooltipPrimitive.Trigger>
        <TooltipPrimitive.Portal>
          <TooltipPrimitive.Content
            sideOffset={5}
            className="z-50 overflow-hidden rounded-md bg-gray-900 px-3 py-1.5 text-xs text-gray-50 animate-in fade-in-0 zoom-in-95 dark:bg-gray-50 dark:text-gray-900"
          >
            {text}
            <TooltipPrimitive.Arrow className="fill-gray-900 dark:fill-gray-50" />
          </TooltipPrimitive.Content>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
}
