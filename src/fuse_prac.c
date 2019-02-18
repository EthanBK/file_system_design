#include <fuse.h>
#include <stdlib.h>
#include <stdio.h>
#include <stddef.h>

static struct options {
    const char * filename;
    const char * contents;
    int show_help;
} options;

// Define marco that returns an array
#define OPTION(t, p)    \
    { t, offsetof(struct options, p), 1 }

// fuse_opt match template
static const struct fuse_opt option_spec[] = {
    OPTION("--name=%s", filename),
	OPTION("--contents=%s", contents),
	OPTION("-h", show_help),
	OPTION("--help", show_help),
	FUSE_OPT_END
};

static void show_help(const char * program_name)
{
    printf("usage: ");
    printf("options:: \n"
           ""
           ""
           ""
           "\n");
}

int main(int argc, char* argv[])
{
    struct fuse_args args = FUSE_ARGS_INIT(argc, argv);

    options.filename = strdup("hello");
    options.contents = strdup("Hello World!");

    if (fuse_opt_parse(&args, &options, option_spec, NULL) == -1) 
        // Error
        return 1;
    
    if (options.show_help) {
        show_help(argv[0]);
        args.argv[0][0] = '\0';
    }

    // return value
    int ret
    ret = fuse_main();

}

