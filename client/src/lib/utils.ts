import { type ClassValue } from "class-variance-authority";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(inputs.filter(Boolean).join(" "));
}
