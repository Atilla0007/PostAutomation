"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { ArrowLeft, Send, CheckCircle, XCircle, Clock } from "lucide-react";
import { AppLayout } from "@/components/layout/app-layout";
import { ProtectedRoute } from "@/components/protected-route";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { postsApi, Post, PostTarget } from "@/lib/api";
import { BackgroundPaths } from "@/components/ui/background-paths";

const statusIcons = {
  selected: Clock,
  queued: Clock,
  rejected: XCircle,
  published: CheckCircle,
};

const statusColors = {
  selected: "text-blue-500",
  queued: "text-yellow-500",
  rejected: "text-red-500",
  published: "text-green-500",
};

export default function PostDetailsPage() {
  const params = useParams();
  const router = useRouter();
  const postId = parseInt(params.id as string);
  const [post, setPost] = useState<Post | null>(null);
  const [loading, setLoading] = useState(true);
  const [publishing, setPublishing] = useState(false);

  useEffect(() => {
    loadPost();
  }, [postId]);

  const loadPost = async () => {
    try {
      // const response = await postsApi.get(postId);
      // setPost(response.data);
      // Mock data for demo
      setPost({
        id: postId,
        content_type: "TEXT",
        caption: "Hello world! This is my first post.",
        hashtags: ["hello", "world"],
        created_at: new Date().toISOString(),
        targets: [
          {
            id: 1,
            social_account_id: 1,
            status: "selected",
          },
          {
            id: 2,
            social_account_id: 2,
            status: "published",
          },
        ],
      });
    } catch (error) {
      console.error("Failed to load post:", error);
    } finally {
      setLoading(false);
    }
  };

  const handlePublish = async () => {
    setPublishing(true);
    try {
      // await postsApi.publish(postId);
      console.log("Publishing post:", postId);
      alert("Post published successfully!");
      loadPost();
    } catch (error: any) {
      console.error("Failed to publish post:", error);
      alert(error.response?.data?.detail || "Failed to publish post");
    } finally {
      setPublishing(false);
    }
  };

  if (loading) {
    return (
      <AppLayout>
        <div className="text-center py-12">Loading post...</div>
      </AppLayout>
    );
  }

  if (!post) {
    return (
      <AppLayout>
        <div className="text-center py-12">Post not found</div>
      </AppLayout>
    );
  }

  return (
    <ProtectedRoute>
      <div className="relative min-h-screen">
        <div className="absolute inset-0 opacity-20">
          <BackgroundPaths title="Post Details" />
        </div>
        <AppLayout>
        <div className="relative z-10 max-w-4xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="mb-6">
              <Button variant="ghost" onClick={() => router.back()} className="mb-4">
                <ArrowLeft className="h-4 w-4 mr-2" />
                Back
              </Button>
            </div>

            <Card className="backdrop-blur-md bg-white/95 dark:bg-black/95 border border-black/10 dark:border-white/10 shadow-xl">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-3xl font-bold mb-2">
                      Post #{post.id}
                    </CardTitle>
                    <CardDescription>
                      Created {new Date(post.created_at).toLocaleString()}
                    </CardDescription>
                  </div>
                  <span className="px-3 py-1 rounded-full bg-muted text-sm capitalize">
                    {post.content_type}
                  </span>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                {/* Content */}
                <div>
                  <h3 className="font-semibold mb-2">Caption</h3>
                  <p className="text-muted-foreground whitespace-pre-wrap">{post.caption}</p>
                </div>

                {/* Hashtags */}
                {post.hashtags.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-2">Hashtags</h3>
                    <div className="flex flex-wrap gap-2">
                      {post.hashtags.map((tag) => (
                        <span
                          key={tag}
                          className="px-3 py-1 bg-muted rounded-full text-sm"
                        >
                          #{tag}
                        </span>
                      ))}
                    </div>
                  </div>
                )}

                {/* Media Preview */}
                {post.image_file && (
                  <div>
                    <h3 className="font-semibold mb-2">Image</h3>
                    <img
                      src={post.image_file}
                      alt="Post"
                      className="rounded-lg max-w-full h-auto"
                    />
                  </div>
                )}

                {post.video_file && (
                  <div>
                    <h3 className="font-semibold mb-2">Video</h3>
                    <video
                      src={post.video_file}
                      controls
                      className="rounded-lg max-w-full"
                    />
                  </div>
                )}

                {/* Targets */}
                {post.targets && post.targets.length > 0 && (
                  <div>
                    <h3 className="font-semibold mb-4">Publishing Targets</h3>
                    <div className="space-y-2">
                      {post.targets.map((target) => {
                        const StatusIcon = statusIcons[target.status];
                        return (
                          <div
                            key={target.id}
                            className="flex items-center justify-between p-3 border rounded-lg"
                          >
                            <div className="flex items-center gap-3">
                              <StatusIcon
                                className={`h-5 w-5 ${statusColors[target.status]}`}
                              />
                              <div>
                                <p className="font-medium">Account #{target.social_account_id}</p>
                                <p className="text-sm text-muted-foreground capitalize">
                                  {target.status}
                                </p>
                              </div>
                            </div>
                            {target.last_error && (
                              <p className="text-sm text-red-500">{target.last_error}</p>
                            )}
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex gap-4 pt-4 border-t">
                  <Button
                    onClick={handlePublish}
                    disabled={publishing}
                    className="gap-2"
                  >
                    <Send className="h-4 w-4" />
                    {publishing ? "Publishing..." : "Publish Now"}
                  </Button>
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

