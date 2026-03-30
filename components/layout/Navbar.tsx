import Link from "next/link";

export default function Navbar() {
  return (
    <header className="sticky top-0 z-50 border-b border-white/10 bg-[#07111f]/80 backdrop-blur-xl">
      <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-4">
        <Link href="/" className="text-xl font-semibold tracking-wide">
          Astra Signum
        </Link>

        <nav className="flex items-center gap-6 text-sm text-slate-300">
          <Link href="/">Home</Link>
          <Link href="/api/videos">API</Link>
        </nav>
      </div>
    </header>
  );
}