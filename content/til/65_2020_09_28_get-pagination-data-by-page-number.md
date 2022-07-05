title: Get pagination data by page number
date: September 28th, 2020
slug: get-pagination-data-by-page-number
category: Laravel
status: active

By default, Laravel's paginator checks the value of the page based on the query string and uses that to display the results and also, it generates links to previous and next pages as well.

The `paginate()` method takes the following parameters by default:
<pre>
<code class="php">
public function paginate($perPage = null, $columns = ['*'], $pageName = 'page', $page = null);
</code>
</pre>

So, if you want to fetch the pagination data of a specific page, then just write this:
<pre>
<code class="php">
$pageNumber = 5;
$data = ExampleModel::paginate(5, ['*'], 'page', $pageNumber);
</code>
</pre>

Hope you found this article useful!