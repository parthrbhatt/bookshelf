
function isBookGenre(genreList, queryGenre) {

  var genreList = genreList.split(",");
  for (var i=0; i<genreList.length; i++)
  {
    if (queryGenre == genreList[i])
      return true;
  }
  return false;
}

function loadBooks() {

  var selectedGenre = document.getElementById("genre").value;
  var bookData = "";
  var count = 0;

  console.log('Showing genre: ' + selectedGenre);
  for (var i=1;i<=NUM_BOOKS;i++)
  {
    book = BOOKS[i];
    if (!(selectedGenre == "All" || isBookGenre(book["genre"], selectedGenre)))
    	continue;

    count += 1;
    bookData += '<DIV class="col-xs-4 col-md-2 parent">\n';
    if (book["review"])
    {
      bookData += '\t<A href="' + book["review"] + '"><IMG src="' + book["image"] + '" class="img-responsive book" /></A>\n';
      bookData += '\t<DIV class="bookreviewed"> REVIEWED </DIV>\n';
    } else {
      bookData += '\t<IMG src="' + book["image"] + '" class="img-responsive book" />\n';
    }
    bookData += '</DIV>\n';

    if (count % 3 == 0)
    {
      if (count % 6 == 0)
      { /* Add the shelf. */
        bookData += '<DIV class="col-xs-12 shelf"></DIV>\n';
      } else {
        /* Add the shelf for smaller screens. */
        bookData += '<DIV class="col-xs-12 shelf hidden-md hidden-lg"></DIV>\n';
      }
    }
  }
  console.log('Displayed ' + count + ' book(s).');

  /* At this point, we are done displaying all the books we had to display.
     If required, fill empty books to complete the shelf */
  if (count % 6 != 0)
  {
    while (count % 6 != 0)
    {
      //console.log('Added Empty Book.');
      bookData += '<DIV class="col-xs-4 col-md-2 parent"></DIV>';
      count += 1;
      if (count % 6 == 0)
      { /* Add the shelf. */
        bookData += '<DIV class="col-xs-12 shelf"></DIV>\n';
      }
    }
  }

  document.getElementById("bookData").innerHTML = bookData;
}
