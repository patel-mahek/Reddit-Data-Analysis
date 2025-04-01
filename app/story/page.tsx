import type { Metadata } from "next"

export const metadata: Metadata = {
  title: "Story | My Website",
  description: "Read my story",
}

export default function StoryPage() {
  return (
    <div className="min-h-screen flex flex-col">
      <div
        className="h-[50vh] bg-cover bg-center bg-fixed flex items-center justify-center"
        style={{
          backgroundImage: "url('/placeholder.svg?height=1080&width=1920')",
          backgroundSize: "cover",
        }}
      >
        <div className="bg-black/50 p-8 md:p-12 rounded-lg max-w-3xl text-center">
          <h1 className="text-3xl md:text-5xl font-bold text-white mb-4">The Journey Begins</h1>
          <p className="text-lg md:text-xl text-white/90">A tale of adventure, discovery, and transformation</p>
        </div>
      </div>

      <div className="container mx-auto px-4 py-12 max-w-3xl">
        <article className="prose prose-lg dark:prose-invert mx-auto">
          <p className="text-xl font-medium">
            It was a crisp autumn morning when I decided to embark on this journey. The leaves were just beginning to
            turn, painting the landscape in hues of amber and gold.
          </p>

          <p>
            Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nullam auctor, nisl eget ultricies tincidunt, nisl
            nisl aliquam nisl, eget ultricies nisl nisl eget nisl. Nullam auctor, nisl eget ultricies tincidunt, nisl
            nisl aliquam nisl, eget ultricies nisl nisl eget nisl.
          </p>

          <h2>The Beginning</h2>
          <p>
            Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec velit neque,
            auctor sit amet aliquam vel, ullamcorper sit amet ligula. Curabitur aliquet quam id dui posuere blandit.
            Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Curabitur non nulla sit amet nisl
            tempus convallis quis ac lectus.
          </p>

          <p>
            Praesent sapien massa, convallis a pellentesque nec, egestas non nisi. Curabitur non nulla sit amet nisl
            tempus convallis quis ac lectus. Vivamus magna justo, lacinia eget consectetur sed, convallis at tellus.
            Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Donec velit neque,
            auctor sit amet aliquam vel, ullamcorper sit amet ligula.
          </p>

          <blockquote>"The journey of a thousand miles begins with a single step." - Lao Tzu</blockquote>

          <h2>The Challenge</h2>
          <p>
            Nulla porttitor accumsan tincidunt. Curabitur aliquet quam id dui posuere blandit. Curabitur arcu erat,
            accumsan id imperdiet et, porttitor at sem. Vivamus magna justo, lacinia eget consectetur sed, convallis at
            tellus. Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui.
          </p>

          <p>
            Donec sollicitudin molestie malesuada. Donec rutrum congue leo eget malesuada. Nulla quis lorem ut libero
            malesuada feugiat. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Sed porttitor lectus
            nibh.
          </p>

          <h2>The Transformation</h2>
          <p>
            Curabitur arcu erat, accumsan id imperdiet et, porttitor at sem. Vivamus suscipit tortor eget felis
            porttitor volutpat. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus. Praesent sapien
            massa, convallis a pellentesque nec, egestas non nisi. Vestibulum ante ipsum primis in faucibus orci luctus
            et ultrices posuere cubilia Curae; Donec velit neque, auctor sit amet aliquam vel, ullamcorper sit amet
            ligula.
          </p>

          <p>
            Pellentesque in ipsum id orci porta dapibus. Donec rutrum congue leo eget malesuada. Vivamus magna justo,
            lacinia eget consectetur sed, convallis at tellus. Curabitur non nulla sit amet nisl tempus convallis quis
            ac lectus. Curabitur non nulla sit amet nisl tempus convallis quis ac lectus.
          </p>

          <h2>The Resolution</h2>
          <p>
            Vestibulum ac diam sit amet quam vehicula elementum sed sit amet dui. Vivamus magna justo, lacinia eget
            consectetur sed, convallis at tellus. Curabitur aliquet quam id dui posuere blandit. Mauris blandit aliquet
            elit, eget tincidunt nibh pulvinar a. Curabitur aliquet quam id dui posuere blandit.
          </p>

          <p>
            And so, as the sun set on this chapter of my journey, I found myself transformed in ways I never could have
            imagined. The path ahead was still uncertain, but I faced it with newfound courage and wisdom.
          </p>
        </article>
      </div>
    </div>
  )
}

