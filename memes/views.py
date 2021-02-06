from django.views import View
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from memes.models import Meme, Comment

import json


class MemeView(View):

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super(MemeView, self).dispatch(*args, **kwargs)

    def get(self, request, meme_id=None):

        if meme_id is None:
            meme_list = []

            for meme in Meme.objects.order_by("-modified")[:100]:
                comment_list = []
                for comment in Comment.objects.order_by("-created").filter(meme_id=meme.id):
                    comment_data = {
                        "id": comment.id,
                        "name": comment.name,
                        "content": comment.content
                    }
                    comment_list.append(comment_data)

                meme_data = {
                    "id": meme.id,
                    "name": meme.name,
                    "url": meme.url,
                    "caption": meme.caption,
                    "likes": meme.likes,
                    "comments": comment_list,
                }
                meme_list.append(meme_data)

            return HttpResponse(json.dumps(meme_list), content_type="application/json")

        else:

            try:
                meme = Meme.objects.get(id=meme_id)
            except:
                return HttpResponse("Meme not found - Task failed successfully", status=404)

            comment_list = []
            for comment in Comment.objects.order_by("-created").filter(meme_id=meme.id):
                comment_data = {
                    "id": comment.id,
                    "name": comment.name,
                    "content": comment.content
                }
                comment_list.append(comment_data)

            meme_data = {
                "id": meme.id,
                "name": meme.name,
                "url": meme.url,
                "caption": meme.caption,
                "likes": meme.likes,
                "comments": comment_list,
            }
            return HttpResponse(
                json.dumps(meme_data), content_type="application/json"
            )

    def post(self, request):
        post_data = json.loads(request.body)

        if Meme.objects.filter(name=post_data["name"], caption=post_data["caption"], url=post_data["url"]).exists():
            return HttpResponse("Meme already exists - Duplicates, Duplicates Everywhere", status=409)

        meme = Meme(name=post_data["name"], caption=post_data["caption"], url=post_data["url"])
        meme.save()
        return HttpResponse(
            json.dumps({
                "id": meme.id
            }), content_type="application/json"
        )
