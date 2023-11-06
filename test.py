import lyricsgenius

TOKEN = "Nh9n4v0Glc6tv2cx4XMzDSZIdzP_Mey9Z_HxI5XTqeJbVsTzEYZx70XhGcQTT0Fn"
CLIENT_ID = "CFdNk_V4aAHysUBHZKknH7ixw91TmC_-_Y2-EUD4T8xpVTs2vu_MRYjL7ii_hIHN"
CLIENT_SECRET = "Ik3bfMkl095vYvlfBlr2Zjt2Q6LIrzDMyhQfZ3RFqcW6dnVTbsKy1XYVuOULhnhtOi7CsLNKglcCEmV0yu98Bw"

genius = lyricsgenius.Genius(TOKEN)

song = genius.search_song("jovail freddy klas")
print(song.lyrics)
