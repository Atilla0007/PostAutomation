"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Link2, Check, X, AlertCircle } from "lucide-react";
import { AppLayout } from "@/components/layout/app-layout";
import { ProtectedRoute } from "@/components/protected-route";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { BackgroundPaths } from "@/components/ui/background-paths";

interface SocialAccount {
  id: number;
  platform: string;
  display_name: string;
  account_type?: string;
  connected: boolean;
  status: "connected" | "disconnected" | "error";
}

const platformIcons: Record<string, string> = {
  instagram: "📷",
  facebook: "👥",
  tiktok: "🎵",
  youtube: "▶️",
  linkedin: "💼",
  x: "🐦",
};

export default function SettingsPage() {
  const [accounts, setAccounts] = useState<SocialAccount[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAccounts();
  }, []);

  const loadAccounts = async () => {
    // Mock data for demo
    setAccounts([
      {
        id: 1,
        platform: "instagram",
        display_name: "My Instagram",
        account_type: "Professional",
        connected: true,
        status: "connected",
      },
      {
        id: 2,
        platform: "facebook",
        display_name: "My Facebook Page",
        connected: true,
        status: "connected",
      },
      {
        id: 3,
        platform: "youtube",
        display_name: "My YouTube Channel",
        connected: false,
        status: "disconnected",
      },
      {
        id: 4,
        platform: "tiktok",
        display_name: "My TikTok",
        connected: false,
        status: "disconnected",
      },
      {
        id: 5,
        platform: "linkedin",
        display_name: "My LinkedIn",
        connected: false,
        status: "disconnected",
      },
      {
        id: 6,
        platform: "x",
        display_name: "My X Account",
        connected: false,
        status: "disconnected",
      },
    ]);
    setLoading(false);
  };

  const handleConnect = (platform: string) => {
    // In production, this would trigger OAuth flow
    alert(`Connecting to ${platform}...`);
  };

  return (
    <ProtectedRoute>
      <div className="relative min-h-screen">
        <div className="absolute inset-0 opacity-20">
          <BackgroundPaths title="Settings" />
        </div>
        <AppLayout>
        <div className="relative z-10 max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <Card className="backdrop-blur-md bg-white/95 dark:bg-black/95 border border-black/10 dark:border-white/10 shadow-xl">
              <CardHeader>
                <CardTitle className="text-3xl font-bold">Social Media Connections</CardTitle>
                <CardDescription>
                  Connect your social media accounts to start publishing
                </CardDescription>
              </CardHeader>
              <CardContent>
                {loading ? (
                  <div className="text-center py-12">Loading connections...</div>
                ) : (
                  <div className="space-y-4">
                    {accounts.map((account, index) => (
                      <motion.div
                        key={account.id}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: index * 0.1 }}
                      >
                        <Card>
                          <CardContent className="p-4">
                            <div className="flex items-center justify-between">
                              <div className="flex items-center gap-4">
                                <span className="text-3xl">
                                  {platformIcons[account.platform] || "📱"}
                                </span>
                                <div>
                                  <h3 className="font-semibold capitalize">
                                    {account.platform}
                                  </h3>
                                  <p className="text-sm text-muted-foreground">
                                    {account.display_name}
                                  </p>
                                  {account.account_type && (
                                    <p className="text-xs text-muted-foreground">
                                      {account.account_type}
                                    </p>
                                  )}
                                </div>
                              </div>
                              <div className="flex items-center gap-4">
                                {account.connected ? (
                                  <div className="flex items-center gap-2 text-green-500">
                                    <Check className="h-5 w-5" />
                                    <span className="text-sm">Connected</span>
                                  </div>
                                ) : (
                                  <Button
                                    onClick={() => handleConnect(account.platform)}
                                    className="gap-2"
                                  >
                                    <Link2 className="h-4 w-4" />
                                    Connect
                                  </Button>
                                )}
                              </div>
                            </div>
                          </CardContent>
                        </Card>
                      </motion.div>
                    ))}
                  </div>
                )}

                <div className="mt-6 p-4 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="h-5 w-5 text-blue-600 dark:text-blue-400 mt-0.5" />
                    <div>
                      <p className="text-sm font-medium text-blue-900 dark:text-blue-100">
                        Connection Requirements
                      </p>
                      <p className="text-xs text-blue-700 dark:text-blue-300 mt-1">
                        Some platforms require specific account types or permissions. Make sure to
                        connect the correct account type for each platform.
                      </p>
                    </div>
                  </div>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </AppLayout>
    </div>
    </ProtectedRoute>
  );
}

