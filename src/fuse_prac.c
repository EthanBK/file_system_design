#include <fuse.h>
#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>

static struct options {
    const char * filename;
    const char * contents;
    int show_help;
} options;

static const struct fuse_opt option_spec[] = {

};



int main(int argc, char* argv[])
{
    struct fuse_args args = FUSE_ARGS_INIT(argc, argv);

    options.filename = strdup("hello");
    options.contents = strdup("Hello World!");

    if (fuse_opt_parse(&args, &options, option_spec, NULL) == -1) 
        // Error
        return 1;

}

