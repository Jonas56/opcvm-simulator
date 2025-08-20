import * as React from "react";
import { cn } from "../../lib/utils";

export function Separator({
  className,
  orientation = "horizontal",
  ...props
}: React.HTMLAttributes<HTMLDivElement> & {
  orientation?: "horizontal" | "vertical";
}) {
  return (
    <div
      className={cn(
        "shrink-0 bg-neutral-200 dark:bg-neutral-800",
        orientation === "horizontal" ? "h-px w-full" : "h-full w-px",
        className
      )}
      role="separator"
      aria-orientation={orientation}
      {...props}
    />
  );
}
