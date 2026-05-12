import "./globals.css";

export const metadata = {
  title: "Enterprise Incentive Intelligence System",
  description: "Enterprise dashboard",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
