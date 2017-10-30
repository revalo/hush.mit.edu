if __name__ == '__main__':
    from confess.models import db
    from confess.models.post import Post
    from confess.models.vote import Vote

    if raw_input('r u sure? ') == 'y':
        Vote.query.delete()
        Post.query.delete()
    db.session.commit()