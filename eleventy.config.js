module.exports = function (eleventyConfig) {
  eleventyConfig.addPassthroughCopy("src/assets");
  eleventyConfig.addPassthroughCopy("src/images");

  eleventyConfig.addCollection("guides", (collectionApi) =>
    collectionApi.getFilteredByGlob("src/guides/*.md").sort((a, b) => b.date - a.date)
  );

  // Short date filter, e.g. "22 Nov 2026" (local time, as Eleventy parses the date)
  eleventyConfig.addFilter("readableDate", (date) => {
    if (!date) return "";
    return new Date(date).toLocaleDateString("en-US", {
      day: "numeric",
      month: "short",
      year: "numeric",
    });
  });

  // ISO date for sitemaps, e.g. "2026-11-22"
  eleventyConfig.addFilter("isoDate", (date) => {
    if (!date) return "";
    const d = new Date(date);
    const p = (n) => String(n).padStart(2, "0");
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
  });

  // Project GitHub Pages serves the site at /gamenightguide/, so every
  // root-absolute link (href="/guides/", src="/assets/...") must be
  // rewritten to /gamenightguide/... in the built HTML. The transform
  // covers links written by hand in templates and Markdown, which the
  // `url` filter does not touch. Links already carrying the prefix are
  // left alone, and protocol-relative URLs (//...) are never touched.
  eleventyConfig.addTransform("prefix-links", function (content) {
    if (!this.page || !this.page.outputPath || !this.page.outputPath.endsWith(".html")) {
      return content;
    }
    return content.replace(
      /(href|src)="\/((?!gamenightguide\/)[^"]*)/g,
      '$1="/gamenightguide/$2'
    );
  });

  return {
    dir: {
      input: "src",
      output: "_site",
      includes: "_includes",
      data: "_data",
    },
    markdownTemplateEngine: "njk",
    htmlTemplateEngine: "njk",
    // Project Pages URL: https://raihanlite.github.io/gamenightguide/
    // Verified with Eleventy 3.1.8: pathPrefix makes page.url include
    // the prefix (so canonical/sitemap/feed URLs are correct) but the
    // built files still land at _site/ root, so the deploy workflow
    // uploads _site as the Pages artifact, unchanged.
    pathPrefix: "/gamenightguide/",
  };
};
