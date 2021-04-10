from typing import Any, Dict, List, Type

from ariadne import SchemaBindable, SchemaDirectiveVisitor

from .action import ActionHook
from .convertblockasttorichtext import ConvertBlockAstToRichTextHook
from .convertinlineasttotext import ConvertInlineAstToTextHook
from .convertrichtextblocktohtml import ConvertRichTextBlockToHTMLHook
from .convertrichtexttohtml import ConvertRichTextToHTMLHook
from .createmarkdown import CreateMarkdownHook
from .createpost import CreatePostHook
from .createthread import CreateThreadHook
from .createuser import CreateUserHook
from .deletecategoriescontents import DeleteCategoriesContentsHook
from .deletethreadpost import (
    DeleteThreadPostHook,
    DeleteThreadPostInputModelHook,
    DeleteThreadPostInputPostHook,
    DeleteThreadPostInputThreadHook,
)
from .deletethreadposts import (
    DeleteThreadPostsHook,
    DeleteThreadPostsInputModelHook,
    DeleteThreadPostsInputPostsHook,
    DeleteThreadPostsInputThreadHook,
)
from .deletethreads import (
    DeleteThreadsHook,
    DeleteThreadsInputHook,
    DeleteThreadsInputModelHook,
)
from .editpost import EditPostHook, EditPostInputHook, EditPostInputModelHook
from .editthreadtitle import (
    EditThreadTitleHook,
    EditThreadTitleInputHook,
    EditThreadTitleInputModelHook,
)
from .filter import FilterHook
from .graphqlcontext import GraphQLContextHook
from .markdown import MarkdownHook
from .movecategoriescontents import MoveCategoriesContentsHook
from .movethread import MoveThreadHook, MoveThreadInputHook, MoveThreadInputModelHook
from .movethreads import (
    MoveThreadsHook,
    MoveThreadsInputHook,
    MoveThreadsInputModelHook,
)
from .parsemarkup import ParseMarkupHook
from .postreply import PostReplyHook, PostReplyInputHook, PostReplyInputModelHook
from .postthread import PostThreadHook, PostThreadInputHook, PostThreadInputModelHook
from .registeruser import (
    RegisterUserHook,
    RegisterUserInputHook,
    RegisterUserInputModelHook,
)
from .templatecontext import TemplateContextHook
from .updatemarkupmetadata import UpdateMarkupMetadataHook
from .updatepost import UpdatePostHook

convert_block_ast_to_rich_text_hook = ConvertBlockAstToRichTextHook()
convert_inline_ast_to_text_hook = ConvertInlineAstToTextHook()
convert_rich_text_block_to_html_hook = ConvertRichTextBlockToHTMLHook()
convert_rich_text_to_html_hook = ConvertRichTextToHTMLHook()
create_markdown_hook = CreateMarkdownHook()
create_post_hook = CreatePostHook()
create_thread_hook = CreateThreadHook()
create_user_hook = CreateUserHook()
delete_categories_contents_hook = DeleteCategoriesContentsHook()
delete_thread_post_hook = DeleteThreadPostHook()
delete_thread_post_input_model_hook = DeleteThreadPostInputModelHook()
delete_thread_post_input_post_hook = DeleteThreadPostInputPostHook()
delete_thread_post_input_thread_hook = DeleteThreadPostInputThreadHook()
delete_thread_posts_hook = DeleteThreadPostsHook()
delete_thread_posts_input_model_hook = DeleteThreadPostsInputModelHook()
delete_thread_posts_input_posts_hook = DeleteThreadPostsInputPostsHook()
delete_thread_posts_input_thread_hook = DeleteThreadPostsInputThreadHook()
delete_threads_hook = DeleteThreadsHook()
delete_threads_input_hook = DeleteThreadsInputHook()
delete_threads_input_model_hook = DeleteThreadsInputModelHook()
edit_post_hook = EditPostHook()
edit_post_input_hook = EditPostInputHook()
edit_post_input_model_hook = EditPostInputModelHook()
edit_thread_title_hook = EditThreadTitleHook()
edit_thread_title_input_hook = EditThreadTitleInputHook()
edit_thread_title_input_model_hook = EditThreadTitleInputModelHook()
graphql_admin_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_admin_type_defs_hook: List[str] = []
graphql_admin_types_hook: List[SchemaBindable] = []
graphql_context_hook = GraphQLContextHook()
graphql_directives_hook: Dict[str, Type[SchemaDirectiveVisitor]] = {}
graphql_type_defs_hook: List[str] = []
graphql_types_hook: List[SchemaBindable] = []
jinja2_extensions_hook: List[Any] = []
jinja2_filters_hook: Dict[str, Any] = {}
markdown_hook = MarkdownHook()
move_categories_contents_hook = MoveCategoriesContentsHook()
move_thread_hook = MoveThreadHook()
move_thread_input_hook = MoveThreadInputHook()
move_thread_input_model_hook = MoveThreadInputModelHook()
move_threads_hook = MoveThreadsHook()
move_threads_input_hook = MoveThreadsInputHook()
move_threads_input_model_hook = MoveThreadsInputModelHook()
parse_markup_hook = ParseMarkupHook()
post_reply_hook = PostReplyHook()
post_reply_input_hook = PostReplyInputHook()
post_reply_input_model_hook = PostReplyInputModelHook()
post_thread_hook = PostThreadHook()
post_thread_input_hook = PostThreadInputHook()
post_thread_input_model_hook = PostThreadInputModelHook()
register_user_hook = RegisterUserHook()
register_user_input_hook = RegisterUserInputHook()
register_user_input_model_hook = RegisterUserInputModelHook()
template_context_hook = TemplateContextHook()
update_markup_metadata_hook = UpdateMarkupMetadataHook()
update_post_hook = UpdatePostHook()
