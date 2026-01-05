"use client";

import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { Check, X, AlertCircle, ExternalLink } from "lucide-react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { PlatformAvailability, AccountAvailability } from "@/lib/api";
import { cn } from "@/lib/utils";

interface PlatformSelectorProps {
  platforms: PlatformAvailability[];
  selectedAccounts: number[];
  onSelectionChange: (accountIds: number[]) => void;
  contentType: "TEXT" | "PHOTO" | "VIDEO";
}

const platformIcons: Record<string, string> = {
  instagram: "📷",
  facebook: "👥",
  tiktok: "🎵",
  youtube: "▶️",
  linkedin: "💼",
  x: "🐦",
};

const platformColors: Record<string, string> = {
  instagram: "from-purple-500 to-pink-500",
  facebook: "from-blue-500 to-blue-600",
  tiktok: "from-black to-gray-800",
  youtube: "from-red-500 to-red-600",
  linkedin: "from-blue-600 to-blue-700",
  x: "from-black to-gray-900",
};

export function PlatformSelector({
  platforms,
  selectedAccounts,
  onSelectionChange,
  contentType,
}: PlatformSelectorProps) {
  const toggleAccount = (accountId: number) => {
    if (selectedAccounts.includes(accountId)) {
      onSelectionChange(selectedAccounts.filter((id) => id !== accountId));
    } else {
      onSelectionChange([...selectedAccounts, accountId]);
    }
  };

  return (
    <div className="space-y-4">
      <h3 className="text-lg font-semibold">Select Platforms</h3>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {platforms.map((platform) => (
          <PlatformCard
            key={platform.platform}
            platform={platform}
            selectedAccounts={selectedAccounts}
            onToggleAccount={toggleAccount}
            contentType={contentType}
          />
        ))}
      </div>
    </div>
  );
}

function PlatformCard({
  platform,
  selectedAccounts,
  onToggleAccount,
  contentType,
}: {
  platform: PlatformAvailability;
  selectedAccounts: number[];
  onToggleAccount: (id: number) => void;
  contentType: "TEXT" | "PHOTO" | "VIDEO";
}) {
  const hasAvailableAccounts = platform.accounts.some((acc) => acc.available);
  const isDisabled = !hasAvailableAccounts;

  return (
    <Card
      className={cn(
        "relative overflow-hidden transition-all duration-300",
        isDisabled && "opacity-60",
        !isDisabled && "hover:shadow-lg"
      )}
    >
      <div
        className={cn(
          "absolute top-0 left-0 right-0 h-1 bg-gradient-to-r",
          platformColors[platform.platform] || "from-gray-400 to-gray-500"
        )}
      />
      <CardHeader>
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-2">
            <span className="text-2xl">{platformIcons[platform.platform] || "📱"}</span>
            <CardTitle className="text-lg capitalize">{platform.platform}</CardTitle>
          </div>
          {platform.available ? (
            <Check className="h-5 w-5 text-green-500" />
          ) : (
            <X className="h-5 w-5 text-red-500" />
          )}
        </div>
        {platform.reason && (
          <CardDescription className="text-xs text-red-500 mt-2">
            {platform.reason}
          </CardDescription>
        )}
      </CardHeader>
      <CardContent>
        {platform.accounts.length === 0 ? (
          <div className="text-sm text-muted-foreground">
            No accounts connected
          </div>
        ) : (
          <div className="space-y-2">
            {platform.accounts.map((account) => (
              <AccountItem
                key={account.social_account_id}
                account={account}
                isSelected={selectedAccounts.includes(account.social_account_id)}
                onToggle={() => onToggleAccount(account.social_account_id)}
              />
            ))}
          </div>
        )}
        {platform.requires_action && platform.action_hint && (
          <div className="mt-3 p-2 bg-yellow-50 dark:bg-yellow-900/20 rounded-md">
            <div className="flex items-start gap-2">
              <AlertCircle className="h-4 w-4 text-yellow-600 dark:text-yellow-400 mt-0.5" />
              <p className="text-xs text-yellow-800 dark:text-yellow-200">
                {platform.action_hint}
              </p>
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}

function AccountItem({
  account,
  isSelected,
  onToggle,
}: {
  account: AccountAvailability;
  isSelected: boolean;
  onToggle: () => void;
}) {
  return (
    <motion.div
      whileHover={{ scale: 1.02 }}
      whileTap={{ scale: 0.98 }}
    >
      <Button
        variant={isSelected ? "default" : "outline"}
        className={cn(
          "w-full justify-start",
          !account.available && "opacity-50 cursor-not-allowed"
        )}
        onClick={onToggle}
        disabled={!account.available}
      >
        <div className="flex items-center justify-between w-full">
          <span className="text-sm">{account.display_name}</span>
          {isSelected && <Check className="h-4 w-4" />}
        </div>
      </Button>
      {account.reason && !account.available && (
        <p className="text-xs text-muted-foreground mt-1 ml-2">
          {account.reason}
        </p>
      )}
    </motion.div>
  );
}

