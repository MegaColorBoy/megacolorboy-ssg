title: Find the difference between two arrays
date: July 18th, 2020
slug: find-the-difference-between-two-arrays
category: JavaScript
status: active

Finding the difference between two sets i.e. Set A and Set B is basically returning a new set that contains values of Set A that don't exist in Set B or vice-versa.

Here's an example:
<pre>
<code class="js">
var a = [1,2,3,4,5];
var b = [1,1,2,3,4];
</code>
</pre>

I wrote a shorter implementation using JavaScript's `.filter()` method:
<pre>
<code class="js">
function array_diff(a,b){
    return a.filter(i => b.indexOf(i) === -1);
}    
</code>
</pre>

Once you execute this method, you'll get the following as a result:
<pre>
<code class="js">
var c = array_diff(a,b);
console.log(c) // returns [5]
</code>
</pre>

## BONUS: What does the .filter() method do?
This method returns a new array with elements that pass the conditions provided by a callback function.

If the conditions aren't passed, you'll receive an empty array.
    
In this article, `(i => b.indexOf(i) === -1)` is considered as the callback function in which the `i` refers to the index of the current element of array A and is then used as a parameter to check if the element doesn't exist in array B.

The neat thing about this method is that it doesn't mutate on the array that it's being called from.

Read more about [Array.prototype.filter()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Array/filter) on Mozilla's developer documentation.