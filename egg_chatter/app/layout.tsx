"use client";

import { Geist, Geist_Mono } from "next/font/google";
import { useEffect, useState, useTransition } from "react";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const [isPending, startTransition] = useTransition();
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isPending) {
      setLoading(true);
    } else {
      setLoading(false);
    }
  }, [isPending]);

  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased text-[#212322]`}
      >
        {loading && (
          <div className="fixed inset-0 flex justify-center items-center bg-opacity-50 bg-black z-50">
            <div className="border-t-4 border-b-4 border-customYellow w-16 h-16 rounded-full animate-spin"></div>
          </div>
        )}
        
        <div className="flex justify-center items-start min-h-screen dot-patter font text-lg">
          <div className="max-w-lg w-full min-h-screen border-2 bg-white py-10 px-8">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}

