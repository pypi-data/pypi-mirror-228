# AEW

An unofficial basic parser for blog posts on https://allelitewrestling.com.

If they change how the pages load.. this will stop working.

## Example Usage

```
In [1]: from aew import AEW

In [2]: a = AEW()

In [3]: posts = a.get_posts()

In [4]: print(posts[0])
Post(url='https://www.allelitewrestling.com/post/best-of-aew-dynamite-for-july-5-2023', title='Best of AEW Dynamite for July 5, 2023', image_url='https://static.wixstatic.com/media/815952_0d4b056ce8504b21baa6d6982641943e~mv2.jpg/v1/fill/w_1920,h_1080,fp_0.50_0.50,q_90,enc_auto/815952_0d4b056ce8504b21baa6d6982641943e~mv2.jpg', aew=<aew.AEW object at 0x000001D93DFF4C10>)

In [5]: posts[0].date
Out[5]: datetime.date(2023, 7, 5)

```
