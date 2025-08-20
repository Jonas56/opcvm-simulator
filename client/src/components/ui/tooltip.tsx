"use client";

import * as React from "react";
import * as TooltipPrimitive from "@radix-ui/react-tooltip";

export const TooltipProvider = TooltipPrimitive.Provider;
export const Tooltip = TooltipPrimitive.Root;
export const TooltipTrigger = TooltipPrimitive.Trigger;

export const TooltipContent = ({
  className,
  ...props
}: React.ComponentProps<typeof TooltipPrimitive.Content>) => (
  <TooltipPrimitive.Content
    sideOffset={6}
    className={`z-50 overflow-hidden rounded-md border border-neutral-200 bg-white px-3 py-1.5 text-sm text-neutral-900 shadow-md dark:border-neutral-800 dark:bg-neutral-900 dark:text-neutral-50 ${
      className ?? ""
    }`}
    {...props}
  />
);
