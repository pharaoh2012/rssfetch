import fs from 'fs';
import { parseFeed } from 'feedsmith'
async function main() {
    fs.mkdirSync("./out", { recursive: true });
    const rss = JSON.parse(fs.readFileSync("./rss.json", "utf8"));
    // console.log(rss);
    for (const item of rss) {
        try {
            console.log(item);
            await doFetch(item);
        } catch (error) {
            console.error(error);
        }

    }
    //   const rssfetch = await import('./rssfetch.mjs');
    //   rssfetch.default();
}

async function doFetch(item) {
    const res = await fetch(item.url).then(r => r.text());

    if (!item.type || item.type === "rss") {
        fs.writeFileSync(`./out/${item.name}.xml`, res);
        const { format, feed } = parseFeed(res)
        console.log({ format });
        fs.writeFileSync(`./out/${item.name}.json`, JSON.stringify(feed));
    }

    // console.log(feed);
    // console.log(res);
}

main();