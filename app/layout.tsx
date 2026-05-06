import './globals.css'
import { ReactNode } from 'react'
import Navbar from '../components/Navbar'
import Sidebar from '../components/Sidebar'

export const metadata = {
  title: 'Enterprise Incentive Intelligence System',
}

export default function RootLayout({ children }: { children: ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-slate-50 text-slate-800 antialiased dark:bg-slate-950 dark:text-slate-100">
        <div className="min-h-screen bg-[radial-gradient(circle_at_top,_rgba(37,99,235,0.08),_transparent_28%),linear-gradient(180deg,_rgba(248,250,252,1),_rgba(241,245,249,1))] dark:bg-[radial-gradient(circle_at_top,_rgba(37,99,235,0.14),_transparent_28%),linear-gradient(180deg,_rgba(2,6,23,1),_rgba(15,23,42,1))]">
          <div className="mx-auto flex min-h-screen max-w-[1600px]">
            <Sidebar />
            <div className="flex-1">
            <Navbar />
            <main className="p-4 sm:p-6 lg:p-8">{children}</main>
          </div>
          </div>
        </div>
      </body>
    </html>
  )
}
