#include <stdio.h>
#include <stdlib.h>

typedef struct Node
{
    char data;
    struct Node *LChild;
    struct Node *RChild;
}BiTNode,*BiTree;

void init(BiTree *bt)
{
    *bt=(BiTree)malloc(sizeof(BiTNode));
    (*bt)->LChild=NULL;
    (*bt)->RChild=NULL;
}

//先序遍历二叉树
void PreOrder(BiTree bt)
{
    if(bt!=NULL)
    {
        printf("%c",bt->data);
        PreOrder(bt->LChild);
        PreOrder(bt->RChild);
    }
}

//中序遍历二叉树
void inOrder(BiTree bt)
{
    if(bt!=NULL)
    {
        inOrder(bt->LChild);
        printf("%c",bt->data);
        inOrder(bt->RChild);
    }
}

//后序遍历二叉树
void PostOrder(BiTree bt)
{
     if(bt!=NULL)
    {
        PostOrder(bt->LChild);
        PostOrder(bt->RChild);
        printf("%c",bt->data);

    }
}

//叶子
void Leafcount(BiTree bt,int num)
{
    if(bt)
    {
        if(bt->LChild ==NULL && bt->RChild==NULL) 
        {
            num++;
            Leafcount(bt->LChild,num);
            Leafcount(bt->RChild,num);
        }
    printf("%d",num);
    }
}
