"use client";

import { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { Upload, X, FileText, Image, Video } from "lucide-react";
import { AppLayout } from "@/components/layout/app-layout";
import { ProtectedRoute } from "@/components/protected-route";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Textarea } from "@/components/ui/textarea";
import { Label } from "@/components/ui/label";
import { PlatformSelector } from "@/components/platform-selector";
import { BackgroundPaths } from "@/components/ui/background-paths";
import { capabilitiesApi, postsApi, ContentType, PlatformAvailability } from "@/lib/api";

export default function CreatePostPage() {
  const router = useRouter();
  const [contentType, setContentType] = useState<ContentType>("TEXT");
  const [caption, setCaption] = useState("");
  const [hashtags, setHashtags] = useState("");
  const [imageFile, setImageFile] = useState<File | null>(null);
  const [videoFile, setVideoFile] = useState<File | null>(null);
  const [selectedAccounts, setSelectedAccounts] = useState<number[]>([]);
  const [platforms, setPlatforms] = useState<PlatformAvailability[]>([]);
  const [loading, setLoading] = useState(false);
  const [loadingPlatforms, setLoadingPlatforms] = useState(false);

  useEffect(() => {
    loadPlatformAvailability();
  }, [contentType]);

  const loadPlatformAvailability = async () => {
    setLoadingPlatforms(true);
    try {
      const response = await capabilitiesApi.get(contentType);
      setPlatforms(response.data);
    } catch (error) {
      console.error("Failed to load platform availability:", error);
      // Mock data for demo
      setPlatforms([
        {
          platform: "instagram",
          available: true,
          reason: null,
          accounts: [
            { social_account_id: 1, display_name: "My Instagram", available: true, reason: null },
          ],
        },
        {
          platform: "facebook",
          available: true,
          reason: null,
          accounts: [
            { social_account_id: 2, display_name: "My Facebook Page", available: true, reason: null },
          ],
        },
        {
          platform: "youtube",
          available: contentType === "VIDEO",
          reason: contentType !== "VIDEO" ? "YouTube supports video uploads only." : null,
          accounts: [
            {
              social_account_id: 3,
              display_name: "My YouTube Channel",
              available: contentType === "VIDEO",
              reason: contentType !== "VIDEO" ? "YouTube supports video uploads only." : null,
            },
          ],
        },
      ]);
    } finally {
      setLoadingPlatforms(false);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, type: "image" | "video") => {
    const file = e.target.files?.[0];
    if (file) {
      if (type === "image") {
        setImageFile(file);
        setVideoFile(null);
      } else {
        setVideoFile(file);
        setImageFile(null);
      }
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append("content_type", contentType);
      formData.append("caption", caption);
      
      const hashtagArray = hashtags
        .split(",")
        .map((tag) => tag.trim().replace("#", ""))
        .filter((tag) => tag.length > 0);
      formData.append("hashtags", JSON.stringify(hashtagArray));

      if (imageFile) {
        formData.append("image_file", imageFile);
      }
      if (videoFile) {
        formData.append("video_file", videoFile);
      }

      if (selectedAccounts.length > 0) {
        formData.append("target_account_ids", JSON.stringify(selectedAccounts));
      }

      // await postsApi.create(formData);
      // For demo, just redirect
      console.log("Creating post:", { contentType, caption, hashtagArray, selectedAccounts });
      router.push("/dashboard");
    } catch (error: any) {
      console.error("Failed to create post:", error);
      alert(error.response?.data?.detail || "Failed to create post");
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="relative min-h-screen">
        <div className="absolute inset-0 opacity-20">
          <BackgroundPaths title="Create Post" />
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
                <CardTitle className="text-3xl font-bold">Create New Post</CardTitle>
                <CardDescription>
                  Create and schedule your content for multiple platforms
                </CardDescription>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleSubmit} className="space-y-6">
                  {/* Content Type Selection */}
                  <div className="space-y-2">
                    <Label>Content Type</Label>
                    <div className="grid grid-cols-3 gap-4">
                      {[
                        { value: "TEXT", label: "Text", icon: FileText },
                        { value: "PHOTO", label: "Photo", icon: Image },
                        { value: "VIDEO", label: "Video", icon: Video },
                      ].map((type) => {
                        const Icon = type.icon;
                        const isSelected = contentType === type.value;
                        return (
                          <Button
                            key={type.value}
                            type="button"
                            variant={isSelected ? "default" : "outline"}
                            onClick={() => setContentType(type.value as ContentType)}
                            className="h-24 flex flex-col gap-2"
                          >
                            <Icon className="h-6 w-6" />
                            {type.label}
                          </Button>
                        );
                      })}
                    </div>
                  </div>

                  {/* Media Upload */}
                  {contentType === "PHOTO" && (
                    <div className="space-y-2">
                      <Label>Image</Label>
                      <div className="border-2 border-dashed rounded-lg p-6 text-center">
                        {imageFile ? (
                          <div className="space-y-2">
                            <p className="text-sm">{imageFile.name}</p>
                            <Button
                              type="button"
                              variant="outline"
                              size="sm"
                              onClick={() => setImageFile(null)}
                            >
                              <X className="h-4 w-4 mr-2" />
                              Remove
                            </Button>
                          </div>
                        ) : (
                          <div>
                            <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                            <Label htmlFor="image-upload" className="cursor-pointer">
                              <span className="text-sm text-muted-foreground">
                                Click to upload or drag and drop
                              </span>
                            </Label>
                            <Input
                              id="image-upload"
                              type="file"
                              accept="image/*"
                              className="hidden"
                              onChange={(e) => handleFileChange(e, "image")}
                            />
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {contentType === "VIDEO" && (
                    <div className="space-y-2">
                      <Label>Video</Label>
                      <div className="border-2 border-dashed rounded-lg p-6 text-center">
                        {videoFile ? (
                          <div className="space-y-2">
                            <p className="text-sm">{videoFile.name}</p>
                            <Button
                              type="button"
                              variant="outline"
                              size="sm"
                              onClick={() => setVideoFile(null)}
                            >
                              <X className="h-4 w-4 mr-2" />
                              Remove
                            </Button>
                          </div>
                        ) : (
                          <div>
                            <Upload className="h-8 w-8 mx-auto mb-2 text-muted-foreground" />
                            <Label htmlFor="video-upload" className="cursor-pointer">
                              <span className="text-sm text-muted-foreground">
                                Click to upload or drag and drop
                              </span>
                            </Label>
                            <Input
                              id="video-upload"
                              type="file"
                              accept="video/*"
                              className="hidden"
                              onChange={(e) => handleFileChange(e, "video")}
                            />
                          </div>
                        )}
                      </div>
                    </div>
                  )}

                  {/* Caption */}
                  <div className="space-y-2">
                    <Label htmlFor="caption">Caption *</Label>
                    <Textarea
                      id="caption"
                      placeholder="Write your caption here..."
                      value={caption}
                      onChange={(e) => setCaption(e.target.value)}
                      rows={4}
                      required
                    />
                  </div>

                  {/* Hashtags */}
                  <div className="space-y-2">
                    <Label htmlFor="hashtags">Hashtags (comma-separated)</Label>
                    <Input
                      id="hashtags"
                      placeholder="hashtag1, hashtag2, hashtag3"
                      value={hashtags}
                      onChange={(e) => setHashtags(e.target.value)}
                    />
                    <p className="text-xs text-muted-foreground">
                      Separate hashtags with commas. Don't include the # symbol.
                    </p>
                  </div>

                  {/* Platform Selection */}
                  {!loadingPlatforms && (
                    <PlatformSelector
                      platforms={platforms}
                      selectedAccounts={selectedAccounts}
                      onSelectionChange={setSelectedAccounts}
                      contentType={contentType}
                    />
                  )}

                  {/* Submit */}
                  <div className="flex gap-4">
                    <Button
                      type="button"
                      variant="outline"
                      onClick={() => router.back()}
                    >
                      Cancel
                    </Button>
                    <Button type="submit" disabled={loading}>
                      {loading ? "Creating..." : "Create Post"}
                    </Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </AppLayout>
    </div>
    </ProtectedRoute>
  );
}

