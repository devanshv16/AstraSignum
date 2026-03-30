import "./globals.css";
import Navbar from "@/components/layout/Navbar";
import PageContainer from "@/components/layout/PageContainer";

export const metadata = {
  title: "Astra Signum",
  description: "A UFO case explorer built from long-form transcript analysis.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body>
        <Navbar />
        <PageContainer>{children}</PageContainer>
      </body>
    </html>
  );
}