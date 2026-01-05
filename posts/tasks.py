from celery import shared_task


@shared_task
def publish_target(post_target_id):
    return {'post_target_id': post_target_id}
