import clsx from 'clsx';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

const FeatureList = [
  {
    title: 'Backend Service',
    Svg: require('@site/static/img/undraw_docusaurus_mountain.svg').default,
    description: (
      <>
        The <strong>reservation-be</strong> backend service handles all business logic,
        API endpoints, and database operations for resource management and reservations.
      </>
    ),
  },
  {
    title: 'Frontend Application',
    Svg: require('@site/static/img/undraw_docusaurus_tree.svg').default,
    description: (
      <>
        The <strong>reservation-fe</strong> React frontend provides an intuitive
        user interface for managing cloud resources, creating reservations, and configuring webhooks.
      </>
    ),
  },
  {
    title: 'Event Processing',
    Svg: require('@site/static/img/undraw_docusaurus_react.svg').default,
    description: (
      <>
        The <strong>reservation-event-processor</strong> microservice handles asynchronous
        event processing and webhook integrations for seamless resource automation.
      </>
    ),
  },
];

function Feature({Svg, title, description}) {
  return (
    <div className={clsx('col col--4')}>
      <div className="text--center">
        <Svg className={styles.featureSvg} role="img" />
      </div>
      <div className="text--center padding-horiz--md">
        <Heading as="h3">{title}</Heading>
        <p>{description}</p>
      </div>
    </div>
  );
}

export default function HomepageFeatures() {
  return (
    <section className={styles.features}>
      <div className="container">
        <div className="row">
          {FeatureList.map((props, idx) => (
            <Feature key={idx} {...props} />
          ))}
        </div>
      </div>
    </section>
  );
}
