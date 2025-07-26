import React from 'react';

export default function Contact() {
  return (
    <div className="min-h-screen w-screen flex flex-col items-center justify-center bg-background text-foreground">
      <div className="p-8 bg-surface rounded-xl shadow-lg text-center">
        <h1 className="text-3xl font-bold mb-4">Contact Me</h1>
        <p className="text-lg mb-2">Email: <a href="mailto:ruben.jimenezmejias@gmail.com" className="text-blue-500 hover:underline">ruben.jimenezmejias@gmail.com</a></p>
        <p className="text-lg mb-2">YouTube: <a href="https://www.youtube.com/@rubenayla" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">youtube.com/@rubenayla</a></p>
        <p className="text-lg mb-2">X (Twitter): <a href="https://x.com/rubenayla" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">x.com/rubenayla</a></p>
        <p className="text-lg mb-2">LinkedIn: <a href="https://www.linkedin.com/in/rubenayla/" target="_blank" rel="noopener noreferrer" className="text-blue-500 hover:underline">linkedin.com/in/rubenayla/</a></p>
      </div>
    </div>
  );
}
