import ReactMarkdown from "react-markdown"
import Moment from "react-moment"
import { fetchAPI } from "../../lib/api"
import Layout from "../../components/layout"
import NextImage from "../../components/image"
import Seo from "../../components/seo"
import { getStrapiMedia } from "../../lib/media"

const Article = ({ article, categories }) => {
  const imageUrl = getStrapiMedia(article.image)

  const seo = {
    metaTitle: article.title,
    metaDescription: article.description,
    shareImage: article.image,
    article: true,
  }

  return (
    <Layout categories={categories}>
      <Seo seo={seo} />
      <div
        id="banner"
        className="uk-inline uk-height-medium uk-flex uk-flex-center uk-flex-middle uk-background-cover uk-light uk-padding uk-margin"
        data-src={imageUrl}
        data-srcset={imageUrl}
        data-uk-img
      >
        <h1>{article.title}</h1>
        {article.image.caption &&
          <div className="uk-overlay uk-light uk-position-bottom">
            <p> {article.image.caption}</p>
          </div>
        }
      </div>
      <div className="uk-section">
        <div className="uk-container uk-container-small">
          <ReactMarkdown source={article.content} escapeHtml={false} />
          <p className="uk-article-meta">
            كلمات دلالية  {article.tags.split(',').map(tag => {
              return <span className="uk-badge uk-margin-small-right ">{tag}</span>
            })}
          </p>
          <hr className="uk-divider-small" />
          <div className="uk-grid-small uk-flex-left" data-uk-grid="true">
            <div>
              {article.author.picture && (
                <NextImage image={article.author.picture} />
              )}
            </div>
            <div className="uk-width-expand">
              <p className="uk-margin-remove-bottom">
                كتب بواسطة {article.author.name}
              </p>
              <p className="uk-text-meta uk-margin-remove-top">
                <Moment format="MMM Do YYYY">{article.published_at}</Moment>
              </p>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  )
}

export async function getStaticPaths() {
  const articles = await fetchAPI("/articles")

  return {
    paths: articles.map((article) => ({
      params: {
        slug: article.slug,
      },
    })),
    fallback: false,
  }
}

export async function getStaticProps({ params }) {
  const articles = await fetchAPI(`/articles?slug=${params.slug}`)
  const categories = await fetchAPI("/categories")

  return {
    props: { article: articles[0], categories },
    revalidate: 1,
  }
}

export default Article
