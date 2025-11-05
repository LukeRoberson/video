# Maintenance

## Getting New Videos

When new videos are available, run the `scripts/scraper` file.

Set `latest_only` to `true` to get the videos in the 'latest' category.

Set it to `false` to perform a more comprehensive search for videos.

When completed, it will create a `missing_videos.csv` file in `scripts/csv`. Check the contents are right (especially categories which may just say 'latest videos').

On the web page, go to 'admin' and 'list videos' to get a list of these videos to import.

</br></br>


> [!WARNING]
> If new videos don't appear on the home screen as new videos,
> try adding the date to these videos manually.

</br></br>


## Indexes

When new videos have been added, or when there's been a significant change in metadata, the Elasticsearch indexes will need to be updated.

Send an API POST to http://localhost:5000/api/search/reindex to start the process.

</br></br>


## Similarity

When videos are added and metadata is updated, the similarity scores also need to be updated.

To do this, run `scripts/similarity.py`.

</br></br>


> [!NOTE]
> This will take about an hour to run.
