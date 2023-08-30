# ## Classification variations
# # bianry class
# # multi class
# # multi label

# ## variations
# # - open-ended (no enum)
# # - closed-ended (enum)
# # - free text (no function calling)


# default_model_args = {
#     "temperature": 0,
#     "model": "gpt-3.5-turbo",
# }

# function_calling_examples = {
#     "multi_class": {
#         "closed": {
#             "function_name": "example_multi_class_closed",
#             "description": "Example of an closed-ended multi class classification prompt function.",
#             "properties": {
#                 "prediction": {
#                     "type": "string",
#                     "enum": ["A", "B", "C"],
#                 }
#             },
#         },
#         "open": {
#             "function_name": "example_multi_class_open",
#             "description": "Example of an open-ended multi class classification prompt function.",
#             "properties": {
#                 "prediction": {
#                     "type": "string",
#                 },
#             },
#         },
#     },
#     # "multi_label": {
#     #     "closed": {
#     #         "function_name": "example_multi_class_closed",
#     #         "description": "Example of an closed-ended multi class classification prompt function.",
#     #         "properties": {
#     #             "prediction": {"type": "array", "items": {"type": "string"}}
#     #         },
#     #     },
#     # },
# }
