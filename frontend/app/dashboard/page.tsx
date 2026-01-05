"use client";

import { useState, useEffect } from "react";
import Link from "next/link";
import { motion } from "framer-motion";
import { Plus, Eye, Calendar, Image, Video, FileText } from "lucide-react";
import { AppLayout } from "@/components/layout/app-layout";
import { ProtectedRoute } from "@/components/protected-route";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { postsApi, Post } from "@/lib/api";
import { BackgroundPaths } from "@/components/ui/background-paths";

const contentTypeIcons = {
  TEXT: FileText,
  PHOTO: Image,
  VIDEO: Video,
};

const contentTypeColors = {
  TEXT: "bg-blue-500",
  PHOTO: "bg-purple-500",
  VIDEO: "bg-red-500",
};

export default function DashboardPage() {
  const [posts, setPosts] = useState<Post[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadPosts();
  }, []);

  const loadPosts = async () => {
    try {
      // For demo, we'll use mock data
      // const response = await postsApi.list();
      // setPosts(response.data);
      setPosts([
        {
          id: 1,
          content_type: "TEXT",
          caption: "Hello world! This is my first post.",
          hashtags: ["hello", "world"],
          created_at: new Date().toISOString(),
        },
        {
          id: 2,
          content_type: "PHOTO",
          caption: "Beautiful sunset today!",
          hashtags: ["sunset", "nature"],
          image_file: "/images/photo.jpg",
          created_at: new Date().toISOString(),
        },
      ]);
    } catch (error) {
      console.error("Failed to load posts:", error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <ProtectedRoute>
      <div className="relative min-h-screen">
        <div className="absolute inset-0 opacity-30">
          <BackgroundPaths title="Dashboard" />
        </div>
        <AppLayout>
        <div className="relative z-10">
          <div className="flex items-center justify-between mb-8">
            <div>
              <h1 className="text-4xl font-bold mb-2">Your Posts</h1>
              <p className="text-muted-foreground">
                Manage and publish your content across platforms
              </p>
            </div>
            <Link href="/posts/create">
              <Button className="gap-2">
                <Plus className="h-4 w-4" />
                Create Post
              </Button>
            </Link>
          </div>

          {loading ? (
            <div className="text-center py-12">Loading posts...</div>
          ) : posts.length === 0 ? (
            <Card className="text-center py-12">
              <CardContent>
                <p className="text-muted-foreground mb-4">
                  You haven't created any posts yet.
                </p>
                <Link href="/posts/create">
                  <Button>Create Your First Post</Button>
                </Link>
              </CardContent>
            </Card>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {posts.map((post, index) => (
                <PostCard key={post.id} post={post} index={index} />
              ))}
            </div>
          )}
        </div>
      </AppLayout>
    </div>
    </ProtectedRoute>
  );
}

function PostCard({ post, index }: { post: Post; index: number }) {
  const Icon = contentTypeIcons[post.content_type];

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1 }}
    >
      <Card className="hover:shadow-lg transition-shadow">
        <CardHeader>
          <div className="flex items-center justify-between">
            <div className={`p-2 rounded-md ${contentTypeColors[post.content_type]}`}>
              <Icon className="h-5 w-5 text-white" />
            </div>
            <span className="text-xs text-muted-foreground capitalize">
              {post.content_type}
            </span>
          </div>
          <CardTitle className="line-clamp-2">{post.caption}</CardTitle>
          <CardDescription>
            {new Date(post.created_at).toLocaleDateString()}
          </CardDescription>
        </CardHeader>
        <CardContent>
          {post.hashtags.length > 0 && (
            <div className="flex flex-wrap gap-1 mb-4">
              {post.hashtags.map((tag) => (
                <span
                  key={tag}
                  className="text-xs bg-muted px-2 py-1 rounded-md"
                >
                  #{tag}
                </span>
              ))}
            </div>
          )}
          <Link href={`/posts/${post.id}`}>
            <Button variant="outline" className="w-full">
              <Eye className="h-4 w-4 mr-2" />
              View Details
            </Button>
          </Link>
        </CardContent>
      </Card>
    </motion.div>
  );
}

